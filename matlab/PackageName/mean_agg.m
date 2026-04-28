function result = mean_agg(data, column)
    % mean_agg - Average of values in a column.
    %
    % Args:
    %   data: Numeric array or struct array.
    %   column: Field name (for struct data) or empty (for numeric data).
    %
    % Returns:
    %   Mean of values, or 0 if empty.

    if isempty(data)
        result = 0;
        return;
    end

    values = extract_values(data, column);
    values = values(~isnan(values));

    if isempty(values)
        result = 0;
    else
        result = mean(values);
    end
end

function values = extract_values(data, column)
    if isstruct(data)
        values = [data.(column)];
    else
        values = data(:)';
    end
end
